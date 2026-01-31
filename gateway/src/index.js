import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import { spawn } from 'child_process';
import chalk from 'chalk';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
    cors: { origin: "*" }
});

const PORT = 18789;
const PYTHON_BRAIN_PATH = path.resolve(__dirname, '../../agents/python-brain');

// Serve static files for the client dashboard
app.use(express.static(path.resolve(__dirname, '../../client/dist')));
app.use(express.json());

// REST API for health check
app.get('/api/health', (req, res) => {
    res.json({ status: 'online', version: '2.0', timestamp: Date.now() });
});

// REST API to get system status
app.get('/api/status', (req, res) => {
    res.json({
        gateway: 'active',
        connections: io.engine.clientsCount,
        uptime: process.uptime()
    });
});

/**
 * Python Brain Bridge
 * Spawns Python process to execute missions and streams output back to client.
 */
class PythonBridge {
    constructor(socket) {
        this.socket = socket;
        this.process = null;
    }

    executeMission(objective) {
        return new Promise((resolve, reject) => {
            console.log(chalk.yellow('⚡ Spawning Python Brain...'));
            
            this.process = spawn('python3', ['-c', `
import sys
sys.path.insert(0, '${PYTHON_BRAIN_PATH}')
from core.orchestrator import CoreOrchestrator
from core.llm import LLMAdapter

orchestrator = CoreOrchestrator()
result = orchestrator.run_mission("${objective.replace(/"/g, '\\"')}")
print("MISSION_RESULT:" + str(result))
            `], {
                cwd: PYTHON_BRAIN_PATH,
                env: { ...process.env, PYTHONUNBUFFERED: '1' }
            });

            let output = '';
            let errorOutput = '';

            this.process.stdout.on('data', (data) => {
                const chunk = data.toString();
                output += chunk;
                
                // Stream real-time updates to client
                const lines = chunk.split('\n').filter(l => l.trim());
                lines.forEach(line => {
                    // Parse log types from Python output
                    if (line.includes('[*]') || line.includes('→')) {
                        this.socket.emit('neural:update', { 
                            status: 'processing', 
                            log: line.replace(/\[\*\]|\[!\]|→/g, '').trim() 
                        });
                    } else if (line.includes('MISSION_RESULT:')) {
                        const result = line.replace('MISSION_RESULT:', '').trim();
                        this.socket.emit('neural:complete', { result });
                    } else if (line.trim()) {
                        this.socket.emit('neural:log', { message: line });
                    }
                });
            });

            this.process.stderr.on('data', (data) => {
                errorOutput += data.toString();
                this.socket.emit('neural:error', { error: data.toString() });
            });

            this.process.on('close', (code) => {
                console.log(chalk.gray(`Python Brain exited with code ${code}`));
                if (code === 0) {
                    resolve(output);
                } else {
                    reject(new Error(errorOutput || `Process exited with code ${code}`));
                }
            });

            this.process.on('error', (err) => {
                console.error(chalk.red('Failed to spawn Python Brain:'), err);
                reject(err);
            });
        });
    }

    kill() {
        if (this.process) {
            this.process.kill('SIGTERM');
            this.process = null;
        }
    }
}

// Active mission bridges (one per socket connection)
const activeBridges = new Map();

io.on('connection', (socket) => {
    console.log(chalk.green('✓ Neural Link Status: CONNECTED'), socket.id);
    
    // Create bridge for this connection
    const bridge = new PythonBridge(socket);
    activeBridges.set(socket.id, bridge);

    socket.on('mission:start', async (data) => {
        console.log(chalk.cyan('→ Mission Objective Received:'), data.objective);
        
        socket.emit('neural:update', { 
            status: 'initializing', 
            log: 'Neural Engine starting...' 
        });

        try {
            const result = await bridge.executeMission(data.objective);
            socket.emit('mission:complete', { 
                success: true, 
                result: result 
            });
        } catch (error) {
            console.error(chalk.red('Mission Error:'), error.message);
            socket.emit('mission:complete', { 
                success: false, 
                error: error.message 
            });
        }
    });

    socket.on('mission:abort', () => {
        console.log(chalk.yellow('⚠ Mission Abort Requested'));
        bridge.kill();
        socket.emit('neural:update', { status: 'aborted', log: 'Mission terminated by operator.' });
    });

    socket.on('command:execute', async (data) => {
        // Direct command execution (for terminal interface)
        console.log(chalk.cyan('→ Direct Command:'), data.command);
        
        const proc = spawn('bash', ['-c', data.command], {
            cwd: data.cwd || process.cwd(),
            timeout: 30000
        });

        let output = '';
        proc.stdout.on('data', (chunk) => {
            output += chunk.toString();
            socket.emit('command:output', { chunk: chunk.toString() });
        });
        proc.stderr.on('data', (chunk) => {
            output += chunk.toString();
            socket.emit('command:output', { chunk: chunk.toString(), isError: true });
        });
        proc.on('close', (code) => {
            socket.emit('command:complete', { code, output });
        });
    });

    socket.on('disconnect', () => {
        console.log(chalk.gray('○ Neural Link Disconnected'), socket.id);
        bridge.kill();
        activeBridges.delete(socket.id);
    });
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log(chalk.yellow('\n⚠ Shutting down gateway...'));
    activeBridges.forEach(bridge => bridge.kill());
    httpServer.close(() => {
        console.log(chalk.gray('Gateway closed.'));
        process.exit(0);
    });
});

httpServer.listen(PORT, () => {
    console.log(chalk.cyan(`\n🦂 STINGBOT GATEWAY ACTIVE`));
    console.log(chalk.gray(`→ Control Plane: http://localhost:${PORT}`));
    console.log(chalk.gray(`→ WebSocket: ws://localhost:${PORT}`));
    console.log(chalk.gray(`→ Python Brain: ${PYTHON_BRAIN_PATH}`));
});
