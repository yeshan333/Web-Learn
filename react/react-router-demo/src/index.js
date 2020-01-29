import React from 'react'
import ReactDOM from 'react-dom'
//import AppRouter from './App'
import AuthExample from './Auth'
import BasicExample from './BasicExample'

/* const Test = ({component: Component}) => (
    <Component/>
);

const Hello = <h1>Hello World</h1> */

//Error: Element type is invalid: expected a string (for built-in components) or
//a class/function (for composite components) but got: object.
//ReactDOM.render(<Test component={Hello}/>, document.getElementById('root'));

ReactDOM.render(<AuthExample/>, document.getElementById('root'));