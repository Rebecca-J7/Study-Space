// import Link from "next/link";

const Footer = () => {
  return (
    <footer className="w-full py-8">
      <div className="mx-auto flex max-w-4xl flex-col items-center gap-3">
        <p className="text-web-purple-2 text-xs">
          © {new Date().getFullYear()} Study Space. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
