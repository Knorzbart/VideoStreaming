import React, { useEffect, useState } from 'react';
import Keycloak from 'keycloak-js';
import './App.css';

function App() {
  const [keycloak, setKeycloak] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const kc = new Keycloak({
      url: 'http://localhost:8080/',
      realm: 'myrealm',
      clientId: 'myclient'
    });

    kc.init({ onLoad: 'login-required' }).then(auth => {
      setKeycloak(kc);
      setAuthenticated(auth);
      if (auth) {
        setUsername(kc.tokenParsed.preferred_username);
        fetch('/api/users', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + kc.token
          },
          body: JSON.stringify({ username: kc.tokenParsed.preferred_username })
        });
      }
    });
  }, []);

  const logout = () => {
    if (keycloak) {
      keycloak.logout();
    }
  };

  if (keycloak) {
    if (authenticated) {
      return (
        <div className="App">
          <header className="App-header">
            <h1>Welcome, {username}</h1>
            <button onClick={logout}>Logout</button>
          </header>
        </div>
      );
    }
    return <div>Initializing Keycloak...</div>;
  }
  return <div>Loading...</div>;
}

export default App;
