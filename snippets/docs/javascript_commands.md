# JavaScript Commands and Examples Reference

###### tags: `javascript`, `node`, `npm`, `express`, `react`, `vue`, `angular`, `frontend`, `backend`, `web`, `api`, `async`, `dom`, `events`

## Table of Contents
- [JavaScript Commands and Examples Reference](#javascript-commands-and-examples-reference)
          - [tags: javascript, node, npm, express, react, vue, angular, frontend, backend, web, api, async, dom, events](#tags:-javascript,-node,-npm,-express,-react,-vue,-angular,-frontend,-backend,-web,-api,-async,-dom,-events)
  - [Table of Contents](#table-of-contents)
  - [Node.js and NPM](#nodejs-and-npm)
          - [tags: node, npm, package, dependencies, scripts](#tags:-node,-npm,-package,-dependencies,-scripts)
  - [Express Server](#express-server)
          - [tags: express, server, routes, middleware, api](#tags:-express,-server,-routes,-middleware,-api)
  - [Frontend Framework Commands](#frontend-framework-commands)
          - [tags: react, vue, angular, frontend, cli](#tags:-react,-vue,-angular,-frontend,-cli)
  - [DOM Operations](#dom-operations)
          - [tags: dom, elements, events, manipulation](#tags:-dom,-elements,-events,-manipulation)
  - [Async Operations](#async-operations)
          - [tags: async, promises, callbacks, fetch, ajax](#tags:-async,-promises,-callbacks,-fetch,-ajax)
  - [Array Operations](#array-operations)
          - [tags: arrays, manipulation, iteration, filtering](#tags:-arrays,-manipulation,-iteration,-filtering)
  - [Object Operations](#object-operations)
          - [tags: objects, properties, methods, classes](#tags:-objects,-properties,-methods,-classes)
  - [Testing Commands](#testing-commands)
          - [tags: testing, jest, mocha, cypress, unit-tests](#tags:-testing,-jest,-mocha,-cypress,-unit-tests)
  - [Build Tools](#build-tools)
          - [tags: webpack, babel, bundler, transpiler](#tags:-webpack,-babel,-bundler,-transpiler)
  - [Debugging](#debugging)
          - [tags: debug, console, devtools, troubleshooting](#tags:-debug,-console,-devtools,-troubleshooting)
  - [Error Handling](#error-handling)
          - [tags: errors, exceptions, try-catch, handling](#tags:-errors,-exceptions,-try-catch,-handling)

## Node.js and NPM
###### tags: `node`, `npm`, `package`, `dependencies`, `scripts`

```javascript
// Initialize project
npm init
npm init -y  // Skip questions

// Install packages
npm install package-name
npm i package-name
npm install --save-dev package-name
npm install -g package-name

// Run scripts
npm run script-name
npm start
npm test

// Update packages
npm update
npm update package-name

// List packages
npm list
npm list --depth=0

// Remove packages
npm uninstall package-name
npm remove package-name

// Package versions
npm version patch
npm version minor
npm version major
```

## Express Server
###### tags: `express`, `server`, `routes`, `middleware`, `api`

```javascript
// Basic Express server
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello World');
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Route parameters
app.get('/user/:id', (req, res) => {
    const userId = req.params.id;
    res.json({ userId });
});

// Query parameters
app.get('/search', (req, res) => {
    const query = req.query.q;
    res.json({ query });
});

// POST request
app.post('/api/data', (req, res) => {
    const data = req.body;
    res.json({ received: data });
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});
```

## Frontend Framework Commands
###### tags: `react`, `vue`, `angular`, `frontend`, `cli`

```javascript
// React (Create React App)
npx create-react-app my-app
cd my-app
npm start

// Vue CLI
npm install -g @vue/cli
vue create my-app
cd my-app
npm run serve

// Angular CLI
npm install -g @angular/cli
ng new my-app
cd my-app
ng serve

// Build commands
npm run build  // React
npm run build  // Vue
ng build      // Angular

// Component generation
ng generate component my-component  // Angular
vue create component MyComponent    // Vue
```

## DOM Operations
###### tags: `dom`, `elements`, `events`, `manipulation`

```javascript
// Selecting elements
const element = document.getElementById('id');
const elements = document.getElementsByClassName('class');
const element = document.querySelector('.class');
const elements = document.querySelectorAll('.class');

// Creating elements
const div = document.createElement('div');
div.textContent = 'Hello';
div.innerHTML = '<span>Hello</span>';

// Modifying elements
element.classList.add('class');
element.classList.remove('class');
element.classList.toggle('class');
element.setAttribute('attr', 'value');
element.style.color = 'red';

// Event handling
element.addEventListener('click', (e) => {
    console.log('Clicked!');
});

element.removeEventListener('click', handler);

// Event delegation
document.body.addEventListener('click', (e) => {
    if (e.target.matches('.button')) {
        console.log('Button clicked!');
    }
});

// DOM traversal
element.parentNode
element.children
element.nextSibling
element.previousSibling
element.firstChild
element.lastChild
```

## Async Operations
###### tags: `async`, `promises`, `callbacks`, `fetch`, `ajax`

```javascript
// Promises
const promise = new Promise((resolve, reject) => {
    if (success) {
        resolve('Success!');
    } else {
        reject('Error!');
    }
});

promise
    .then(result => console.log(result))
    .catch(error => console.error(error));

// Async/Await
async function getData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}

// Fetch API
fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

// Axios
axios.get('https://api.example.com/data')
    .then(response => console.log(response.data))
    .catch(error => console.error(error));

// Multiple promises
Promise.all([promise1, promise2])
    .then(results => console.log(results))
    .catch(error => console.error(error));
```

## Array Operations
###### tags: `arrays`, `manipulation`, `iteration`, `filtering`

```javascript
// Array methods
array.map(item => item * 2);
array.filter(item => item > 5);
array.reduce((acc, item) => acc + item, 0);
array.forEach(item => console.log(item));
array.find(item => item.id === 1);
array.some(item => item > 5);
array.every(item => item > 0);

// Array manipulation
array.push(item);
array.pop();
array.shift();
array.unshift(item);
array.splice(index, count, item);
array.slice(start, end);

// Array spread
const newArray = [...array1, ...array2];
const copy = [...array];

// Array destructuring
const [first, second, ...rest] = array;
```

## Object Operations
###### tags: `objects`, `properties`, `methods`, `classes`

```javascript
// Object creation
const obj = {
    prop: value,
    method() {
        return this.prop;
    }
};

// Classes
class MyClass {
    constructor(prop) {
        this.prop = prop;
    }

    method() {
        return this.prop;
    }

    static staticMethod() {
        return 'static';
    }
}

// Object spread
const newObj = { ...obj1, ...obj2 };
const copy = { ...obj };

// Object destructuring
const { prop1, prop2: alias, ...rest } = obj;

// Object methods
Object.keys(obj);
Object.values(obj);
Object.entries(obj);
Object.assign(target, source);
```

## Testing Commands
###### tags: `testing`, `jest`, `mocha`, `cypress`, `unit-tests`

```javascript
// Jest
npm install --save-dev jest
jest
jest --watch
jest --coverage

// Test example
test('adds 1 + 2 to equal 3', () => {
    expect(add(1, 2)).toBe(3);
});

// Mocha
npm install --save-dev mocha
mocha
mocha test/*.js

// Cypress
npm install cypress --save-dev
npx cypress open
npx cypress run
```

## Build Tools
###### tags: `webpack`, `babel`, `bundler`, `transpiler`

```javascript
// Webpack
npm install --save-dev webpack webpack-cli
webpack
webpack --mode production
webpack --watch

// Babel
npm install --save-dev @babel/core @babel/cli
babel src -d dist
babel src -d dist --watch

// ESLint
npm install --save-dev eslint
eslint .
eslint . --fix

// Prettier
npm install --save-dev prettier
prettier --write .
```

## Debugging
###### tags: `debug`, `console`, `devtools`, `troubleshooting`

```javascript
// Console methods
console.log('Message');
console.error('Error');
console.warn('Warning');
console.table(array);
console.time('Label');
console.timeEnd('Label');

// Debugger
debugger;

// Performance
console.time('Operation');
// code to measure
console.timeEnd('Operation');

// Stack trace
console.trace();

// Memory usage
console.memory
```

## Error Handling
###### tags: `errors`, `exceptions`, `try-catch`, `handling`

```javascript
// Try-catch
try {
    // risky code
} catch (error) {
    console.error(error);
} finally {
    // cleanup
}

// Custom error
class CustomError extends Error {
    constructor(message) {
        super(message);
        this.name = 'CustomError';
    }
}

// Async error handling
async function handleErrors() {
    try {
        await riskyOperation();
    } catch (error) {
        console.error(error);
    }
}
