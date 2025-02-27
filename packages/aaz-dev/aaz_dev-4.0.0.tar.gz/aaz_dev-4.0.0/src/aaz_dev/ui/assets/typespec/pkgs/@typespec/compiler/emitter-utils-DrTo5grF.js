import { g as getDirectoryPath } from './path-utils-3cuVtir1.js';

/**
 * Helper to emit a file.
 * @param program TypeSpec Program
 * @param options File Emitter options
 */
async function emitFile(program, options) {
    // ensure path exists
    const outputFolder = getDirectoryPath(options.path);
    await program.host.mkdirp(outputFolder);
    const content = options.newLine && options.newLine === "crlf"
        ? options.content.replace(/(\r\n|\n|\r)/gm, "\r\n")
        : options.content;
    return await program.host.writeFile(options.path, content);
}

export { emitFile as e };
