import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import chalk from 'chalk';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
    cors: { origin: "*" }
});

const PORT = 18789;

io.on('connection', (socket) => {
    console.log(chalk.green('✓ Neural Link Status: CONNECTED'), socket.id);

    socket.on('mission:start', (data) => {
        console.log(chalk.cyan('→ Mission Objective Received:'), data.objective);
        // Bridge to Python Brain will go here
        socket.emit('neural:update', { status: 'Analysing Target...', log: 'Initializing Nmap scan...' });
    });
});

httpServer.listen(PORT, () => {
    console.log(chalk.cyan(`\n🦂 STINGBOT GATEWAY ACTIVE`));
    console.log(chalk.gray(`→ Control Plane: http://localhost:${PORT}`));
});
