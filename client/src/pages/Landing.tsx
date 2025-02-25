import { useState } from "react";

// COMPONENTS
import LoginForm from "../components/forms/LoginForm";
import RegisterForm from "../components/forms/RegisterForm";

function Landing() {
  const [newUser, setNewUser] = useState<boolean>(false);

  const toggleNewUser = () => setNewUser((prev) => !prev);

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col justify-center items-center">
      <h1 className="text-4xl text-white mb-8">Welcome to Rent Receipts</h1>
      {newUser ? <RegisterForm /> : <LoginForm />}
      <button
        onClick={toggleNewUser}
        className="bg-neutral-800 hover:bg-neutral-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        {newUser ? "Back to login" : "Don't have an account? Register"}
      </button>
    </div>
  );
}

export default Landing;
