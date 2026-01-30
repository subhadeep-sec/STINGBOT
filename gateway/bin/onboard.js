#!/usr/bin/env node
import { exec } from 'child_process';
import path from 'path';
import os from 'os';
import chalk from 'chalk';

console.log(chalk.cyan("\n🦂 STINGBOT — NEURAL PLATFORM ONBOARDING"));
console.log(chalk.gray("----------------------------------------\n"));

const installDir = path.join(os.homedir(), 'STINGBOT'); // Keeping path for legacy sync

console.log(chalk.yellow("→ [WIZARD] Provisioning Neural Assets..."));

// Bridge to the existing installer for now
const installer = exec('curl -sSL https://raw.githubusercontent.com/subhadeep-sec/STINGBOT/main/install.sh | bash');

installer.stdout.on('data', (data) => {
    process.stdout.write(data);
});

installer.stderr.on('data', (data) => {
    process.stderr.write(data);
});

installer.on('close', (code) => {
    if (code === 0) {
        console.log(chalk.green("\n✓ [PLATFORM] Stingbot Gateway Established."));
        console.log("→ Run " + chalk.bold("stingbot doctor") + " to verify parity.");
    }
});
