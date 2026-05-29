const express = require('express');
const path = require('path');

const app = express();
const port = 8000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/cart', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'cart.html'));
});


app.listen(port, () => {
    console.log(`\n🍲  Home Kitchen Catering Website`);
    console.log(`   Admin Panel: http://localhost:${port}/admin`);
    console.log(`   Running at: http://localhost:${port}\n`);
});
