import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="container">
        <h1>HR AI Workflow</h1>
        <nav>
          <ul>
            <li>
              <Link to="/">Upload CV</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
