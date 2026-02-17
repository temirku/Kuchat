const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const fs = require('fs');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Соединяем папки
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Простая база сообщений в памяти для начала
let messages = [];

io.on('connection', (socket) => {
    console.log('Пользователь подключился');
    socket.emit('history', messages);

    socket.on('msg', (data) => {
        messages.push(data);
        io.emit('msg', data);
    });
});

server.listen(3000, '0.0.0.0', () => {
    console.log('\n--- СИСТЕМА KBR-AVIA: МОЗГИ И ДИЗАЙН СОЕДИНЕНЫ ---');
    console.log('Адрес: http://localhost:3000');
});
