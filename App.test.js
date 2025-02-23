import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom'; // Import Router
import App from './App';

test('renders MindGuard title', () => {
  render(
    <Router> {/* Wrap with Router for testing */}
      <App />
    </Router>
  );
  const titleElement = screen.getByRole('heading', { name: /MindGuard/i }); // More robust way to find the title
  expect(titleElement).toBeInTheDocument();
});

test('renders login form when not logged in', () => {
    render(
      <Router>
        <App />
      </Router>
    );
    const loginForm = screen.getByRole('form'); // You can also use getByRole('form')
    expect(loginForm).toBeInTheDocument();
  });