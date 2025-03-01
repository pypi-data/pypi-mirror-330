use std::{env, fs::File, hint::black_box, io::Read, vec};

use llguidance::{
    api::{ParserLimits, TopLevelGrammar},
    earley::XorShift,
    lark_to_llguidance,
    toktrie::{InferenceCapabilities, TokEnv},
    Constraint, JsonCompileOptions, TokenParser,
};
use serde_json::json;

fn dump_tokenizer(name: &str) {
    let btok = toktrie_hf_tokenizers::ByteTokenizer::from_name(name).unwrap();
    let vecs = btok.token_bytes();
    for (_i, v) in vecs.iter().enumerate() {
        let v: String = v
            .iter()
            .map(|b| format!("{:02x}", b))
            .collect::<Vec<_>>()
            .join("");
        println!("{}", v);
    }
}

fn main() {
    if false {
        dump_tokenizer("microsoft/Phi-3.5-mini-instruct");
    }

    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <schema.ll.json> <sample.json>", args[0]);
        std::process::exit(1);
    }

    let schema_file = read_file_to_string(&args[1]);
    let schema: TopLevelGrammar = if args[1].ends_with(".ll.json") {
        serde_json::from_str(&schema_file).expect("Invalid JSON in schema")
    } else if args[1].ends_with(".schema.json") {
        let opts = JsonCompileOptions::default();
        let val = serde_json::from_str(&schema_file).expect("Invalid JSON in schema");
        opts.json_to_llg(val)
            .expect("Failed to convert JSON to LLG")
    } else if args[1].ends_with(".lark") {
        lark_to_llguidance(&schema_file).expect("Failed to convert lark to LLG")
    } else if args[1].ends_with(".txt") {
        // assume substring on words
        TopLevelGrammar::from_lark(format!(
            "start: \"foo\" sub\nsub: %regex {}",
            serde_json::to_string(&json!({
                "substring_words": schema_file
            }))
            .unwrap()
        ))
    } else {
        panic!("Unknown schema file extension")
    };

    // you can implement TokEnv yourself, if you have the tokenizer
    // see the ByteTokenizerEnv for an example
    let tok_env: TokEnv =
        toktrie_hf_tokenizers::ByteTokenizerEnv::from_name("microsoft/Phi-3.5-mini-instruct", None)
            .unwrap()
            .to_env();

    // set to 2 for more output; 1 is warnings only
    let stderr_log_level = 1;

    // typically set to 2, to send info-level output to the user
    let buffer_log_level = 2;

    let t0 = std::time::Instant::now();

    let mut limits = ParserLimits::default();
    limits.initial_lexer_fuel *= 1;

    let parser = TokenParser::from_llguidance_json(
        tok_env.clone(),
        schema,
        llguidance::Logger::new(buffer_log_level, stderr_log_level),
        InferenceCapabilities {
            ff_tokens: true,  // can the engine append multiple tokens?
            backtrack: false, // can the engine remove generated tokens?

            conditional_ff_tokens: false, // not used
            fork: false,                  // not used
        },
        ParserLimits::default(),
        vec![],
    )
    .unwrap();
    let mut constraint = Constraint::new(parser);

    // enable sending parser results back via the logs (constraint.flush_logs())
    constraint.log_json_progress = true;

    if args[2] == "SKIP" {
        constraint.start_without_prompt();
        let _ = constraint.compute_mask().unwrap();
        return;
    }

    if args[2].starts_with("RND") {
        let max_tokens = args[2][3..].parse::<usize>().unwrap_or(100);
        constraint.start_without_prompt();
        let mut rng = XorShift::new((max_tokens + 1) as u32);
        let mut tokens = vec![];
        let mut lens = vec![];
        let trie = tok_env.tok_trie();
        let mut prev_time = std::time::Instant::now();
        let mut times = vec![prev_time.duration_since(t0).as_micros() as u64];
        for _ in 0..max_tokens {
            let r = constraint.compute_mask().unwrap();
            times.push(prev_time.elapsed().as_micros() as u64);
            prev_time = std::time::Instant::now();
            if r.is_stop() {
                break;
            }
            let mut v = r.sample_mask.clone().unwrap();
            // mostly disallow eos to make it run longer
            if !rng.one_in(5) {
                v.disallow_token(trie.eos_token());
            }
            let t = rng.sample_from_vob(&v);
            let r = constraint.commit_token(Some(t)).unwrap();
            assert_eq!(r.backtrack, 0);
            tokens.extend_from_slice(&r.ff_tokens);
            lens.push(r.ff_tokens.len());
        }
        eprintln!("Lens: {:?}", lens);
        eprintln!("Tokens:\n{}\n", trie.decode_str(&tokens));
        eprintln!("Mask times: {:?}", times);
        return;
    }

    let trie = tok_env.tok_trie();

    let obj_str = read_file_to_string(&args[2]);
    let tokens = tok_env.tokenize(&obj_str);
    eprintln!("Parsing tokens: {}", trie.tokens_dbg(&tokens));

    // constraint.parser.start_without_prompt();
    // constraint.parser.consume_token(tokens[0]).unwrap();

    let mut idx = 0;
    while idx < tokens.len() {
        let res = constraint.compute_mask().unwrap();

        if res.is_stop() {
            // stop sequence
            break;
        }

        let mut is_allowed = true;

        let sampled_token = if let Some(mask) = &res.sample_mask {
            // Simulate sampling - it should use the mask and temperature
            let sampled_token = tokens[idx];
            is_allowed = mask.is_allowed(sampled_token);
            black_box(mask);
            black_box(constraint.temperature);

            let p_stats = constraint.parser.last_step_stats();
            println!(
                "SAMPLE {}: {} {}; stats: {} lex, {} items, {} us",
                idx,
                sampled_token,
                tok_env.tok_trie().token_dbg(sampled_token),
                p_stats.lexer_cost,
                p_stats.all_items,
                p_stats.compute_time_us,
            );
            Some(sampled_token)
        } else {
            // sampling not required
            println!("NO SAMPLE");
            None
        };

        // run commit_token() before checking the mask - it produces more diagnostics that way
        let splice = constraint.commit_token(sampled_token).unwrap();

        if !is_allowed {
            panic!("Sampled token was not allowed by the mask");
        }

        if splice.stop {
            // stop sequence
            break;
        }

        assert!(splice.backtrack == 0); // we didn't allow backtracking in InferenceCaps

        // The splice contains the tokens (possibly more than one since we enabled ff_tokens
        // in InferenceCaps) that the parser wants to append to the output.

        // if this fails, our test data is broken
        if tokens[idx..idx + splice.ff_tokens.len()] != splice.ff_tokens {
            panic!(
                "BAD TEST: ff_tokens mismatch:\n{}\n{}",
                trie.tokens_dbg(&tokens[idx..idx + splice.ff_tokens.len()]),
                trie.tokens_dbg(&splice.ff_tokens)
            );
        }

        if splice.ff_tokens.len() > 1 {
            println!("FF: {}", trie.tokens_dbg(&splice.ff_tokens));
        }

        idx += splice.ff_tokens.len();

        // send output to the user
        send_output(&constraint.flush_logs());
    }

    // flush any output
    send_output(&constraint.flush_logs());
    // the stop reason should be likely also sent to the user
    println!("Stop reason: {:?}", constraint.parser.stop_reason());

    println!("Max step stats: {:?}", constraint.parser.max_step_stats());
}

fn read_file_to_string(filename: &str) -> String {
    let mut file = File::open(filename).expect("Unable to open file");
    let mut content = String::new();
    file.read_to_string(&mut content)
        .expect("Unable to read file");
    content
}

fn send_output(user_output: &str) {
    // enable if you want to see the output
    if false {
        println!("{}", user_output);
    }
}
