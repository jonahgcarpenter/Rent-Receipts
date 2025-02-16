import { Link } from "react-router-dom";

type PrimaryButtonProps = {
  title: string;
  link: string;
};

const PrimaryButton = ({ title, link }: PrimaryButtonProps) => {
  return (
    <Link
      to={link}
      className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-md transition duration-300 shadow-md"
    >
      {title}
    </Link>
  );
};

export default PrimaryButton;
