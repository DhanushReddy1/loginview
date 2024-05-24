import React, { useState } from 'react';
import PropTypes from 'prop-types';
import styles from './Login.module.css';

function Login() {
   const [email, setEmail] = useState('');
   const [password, setPassword] = useState('');
   async function handleLogin() {
      try {
         const response = await axios.post('/api/login', { email, password });
         localStorage.setItem('token', response.data.token);
         // Redirect to dashboard
      } catch (error) {
         console.error('Error logging in', error);
      }
   }
   return (
      <div>
         <h2>Login</h2>
         <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
         <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
         <button onClick={handleLogin}>Login</button>
      </div>
   );
}

Login.propTypes = {};

Login.defaultProps = {};

export default Login;
