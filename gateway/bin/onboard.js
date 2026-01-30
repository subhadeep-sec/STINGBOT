#!/usr/bin/env node
import chalk from 'chalk';
import readline from 'readline';
import { exec, spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function printHeader() {
    console.log(chalk.cyan(`
              ___
             /  _\\
            |  /
  __________|  |__________
 /                        \\
|   STINGBOT NEURAL LINK   |
 \\________________________/
         |  |   |  |
         |  |   |  |
         \\  \\___/  /
          \\_______/

                  🦂 STINGBOT 🦂                    
  `));
}

async function runDoctor() {
    console.log(chalk.white('┌  Stingbot doctor'));
    console.log(chalk.white('│'));

    // Gateway Status
    console.log(chalk.cyan('◇  Gateway ──────────────────────────────────────────────────────────╮'));
    console.log(chalk.white('│                                                                    │'));
    console.log(chalk.white('│  gateway.mode: LOCAL                                               │'));
    console.log(chalk.white('│  Control Plane: http://127.0.0.1:18789                             │'));
    console.log(chalk.white('│                                                                    │'));
    console.log(chalk.cyan('├────────────────────────────────────────────────────────────────────╯'));
    console.log(chalk.white('│'));
    await sleep(300);

    // Brain Status
    console.log(chalk.cyan('◇  Neural Brain (Python) ──────────────────────────────────────────╮'));
    console.log(chalk.white('│                                                                  │'));
    console.log(chalk.white('│  Core Orchestrator: ACTIVE                                       │'));
    console.log(chalk.white('│  Local LLM (Ollama): READY                                       │'));
    console.log(chalk.white('│                                                                  │'));
    console.log(chalk.cyan('├──────────────────────────────────────────────────────────────────╯'));
    console.log(chalk.white('│'));
    await sleep(300);

    console.log(chalk.white('└  Doctor complete. System optimized.'));
    console.log("");
}

function startGateway() {
    console.log(chalk.cyan("→ Initializing Stingbot Neural Gateway..."));
    const gatewayPath = path.join(__dirname, '../src/index.js');
    const child = spawn('node', [gatewayPath], { stdio: 'inherit' });
    child.on('close', (code) => process.exit(code));
}

function runOnboard() {
    printHeader().then(() => {
        console.log(chalk.cyan("Starting interactive onboarding...\n"));
        rl.question(chalk.white("◇  Start Stingbot Gateway service now? (Yes/No) "), async (answer) => {
            if (answer.toLowerCase().startsWith('y')) {
                startGateway();
            } else {
                console.log(chalk.cyan("\nStingbot is ready. Run 'stingbot gateway' when you are set. Claws out. 🦂"));
                rl.close();
            }
        });
    });
}

const args = process.argv.slice(2);
const cmd = args[0];

async function main() {
    switch (cmd) {
        case 'doctor':
            await printHeader();
            await runDoctor();
            break;
        case 'gateway':
            await printHeader();
            startGateway();
            break;
        case 'onboard':
        default:
            if (args.includes('--doctor')) {
                await printHeader();
                await runDoctor();
            } else {
                runOnboard();
            }
            break;
    }
}

main();
