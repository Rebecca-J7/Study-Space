/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  trailingSlash: true,
  output: "standalone",  // ← add this
  images: {
    unoptimized: true,
  },
};

export default nextConfig;

