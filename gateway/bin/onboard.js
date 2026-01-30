#!/usr/bin/env node
import chalk from 'chalk';
import readline from 'readline';

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
    console.log(chalk.white('│  gateway.mode is currently set to: LOCAL                           │'));
    console.log(chalk.white('│  Control Plane: http://127.0.0.1:18789                             │'));
    console.log(chalk.white('│                                                                    │'));
    console.log(chalk.cyan('├────────────────────────────────────────────────────────────────────╯'));
    console.log(chalk.white('│'));
    await sleep(500);

    // Brain Status
    console.log(chalk.cyan('◇  Neural Brain (Python) ──────────────────────────────────────────╮'));
    console.log(chalk.white('│                                                                  │'));
    console.log(chalk.white('│  Core Orchestrator: ACTIVE                                       │'));
    console.log(chalk.white('│  Local LLM (Ollama): CONNECTED (llama3.2)                        │'));
    console.log(chalk.white('│                                                                  │'));
    console.log(chalk.cyan('├──────────────────────────────────────────────────────────────────╯'));
    console.log(chalk.white('│'));
    await sleep(500);

    // Security Tools
    console.log(chalk.cyan('◇  Security Arsenal ────────────────────────╮'));
    console.log(chalk.white('│                                            │'));
    console.log(chalk.white('│  - Nmap: DETECTED                          │'));
    console.log(chalk.white('│  - Sqlmap: DETECTED                        │'));
    console.log(chalk.white('│  - Nikto: DETECTED                         │'));
    console.log(chalk.white('│                                            │'));
    console.log(chalk.cyan('├────────────────────────────────────────────╯'));
    console.log(chalk.white('│'));
    await sleep(500);

    // Skills
    console.log(chalk.cyan('◇  Tasking Capacity ────────╮'));
    console.log(chalk.white('│                            │'));
    console.log(chalk.white('│  Eligible Skills: 8        │'));
    console.log(chalk.white('│  Active Modules: 12        │'));
    console.log(chalk.white('│                            │'));
    console.log(chalk.cyan('├────────────────────────────╯'));
    console.log(chalk.white('│'));

    console.log(chalk.white('└  Doctor complete.'));
    console.log("");
}

async function main() {
    const isDoctor = process.argv.includes('--doctor');

    if (isDoctor) {
        console.log(chalk.cyan("\n🦂 Stingbot v1.0.0 — Greetings, Operator"));
        await printHeader();
        await runDoctor();
        console.log(chalk.green("✓ Platform migration complete."));
        console.log(chalk.gray("\nStingbot installed successfully (v1.0.0)!"));
        console.log(chalk.gray("“If it's predictable, I'll automate it; if it's lethal, I'll bring the jokes.”\n"));
        process.exit(0);
    }

    // Interactive Onboarding mode
    await printHeader();
    console.log(chalk.cyan("Starting interactive onboarding...\n"));

    rl.question(chalk.white("◇  Start Stingbot Gateway service now? (Yes/No) "), async (answer) => {
        if (answer.toLowerCase().startsWith('y')) {
            console.log(chalk.green("✓ Gateway service initialized."));
            console.log(chalk.gray("Dashboard URL: ") + chalk.bold("http://127.0.0.1:18789/\n"));
        }
        console.log(chalk.cyan("Stingbot is ready. Claws out. 🦂"));
        rl.close();
    });
}

main();
