#!/usr/bin/env node
import { exec } from 'child_process';
import path from 'path';
import os from 'os';

const args = process.argv.slice(2);
const installDir = path.join(os.homedir(), 'STINGBOT');
const pythonPath = path.join(installDir, 'main.py');

if (args[0] === 'onboard') {
    console.log("🦂 [WIZARD] Initiating Neural Onboarding...");
    const installer = exec('curl -sSL https://raw.githubusercontent.com/subhadeep-sec/STINGBOT/main/install.sh | bash');
    installer.stdout.pipe(process.stdout);
    installer.stderr.pipe(process.stderr);
} else {
    // Run the Python core
    const cmd = `python3 ${pythonPath} ${args.join(' ')}`;
    const proc = exec(cmd);
    proc.stdout.pipe(process.stdout);
    proc.stderr.pipe(process.stderr);
}
