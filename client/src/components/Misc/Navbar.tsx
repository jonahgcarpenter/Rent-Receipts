import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-purple-500 p-4">
      <ul className="flex space-x-4">
        <li>
          <Link to="/">Home</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
