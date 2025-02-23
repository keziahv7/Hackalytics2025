import React from 'react';

function Signup() {
  return (
    <div>
      <h1>Signup Page</h1>
      <form>
        {/* Basic form structure */}
        <label>
          Username:
          <input type="text" name="username" />
        </label>
        <label>
          Password:
          <input type="password" name="password" />
        </label>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default Signup;
