use re_log_types::LogMsg;
use re_smart_channel::Sender;

/// Asynchronously loads RRD data streaming in from standard input.
///
/// This fails synchronously iff the standard input stream could not be opened, otherwise errors
/// are handled asynchronously (as in: they're logged).
pub fn load_stdin(tx: Sender<LogMsg>) -> anyhow::Result<()> {
    let stdin = std::io::BufReader::new(std::io::stdin());
    let decoder = re_log_encoding::decoder::Decoder::new_concatenated(stdin)?;

    rayon::spawn(move || {
        re_tracing::profile_scope!("stdin");

        for msg in decoder {
            let msg = match msg {
                Ok(msg) => msg,
                Err(err) => {
                    re_log::warn_once!("Failed to decode message in stdin: {err}");
                    continue;
                }
            };
            if tx.send(msg).is_err() {
                break; // The other end has decided to hang up, not our problem.
            }
        }

        tx.quit(None).ok(); // The other end has decided to hang up, not our problem.
    });

    Ok(())
}
