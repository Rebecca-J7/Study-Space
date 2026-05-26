/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: "export",
  reactStrictMode: true,
  trailingSlash: true,
  images: {
    loader: "akamai",
    path: "",
    unoptimized: true,
  },
};

module.exports = nextConfig;
