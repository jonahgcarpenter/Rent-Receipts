// COMPONENTS
import PrimaryButton from "../components/Buttons/PrimaryButton";

function Landing() {
  return (
    <div className="min-h-screen bg-gray-900 flex flex-col justify-center items-center">
      <h1 className="text-4xl text-white mb-8">Welcome to Rent Receipts</h1>
      <div className="flex space-x-4">
        <PrimaryButton title="Sign Up" link="/signup" />
        <PrimaryButton title="Login" link="/login" />
      </div>
    </div>
  );
}

export default Landing;
