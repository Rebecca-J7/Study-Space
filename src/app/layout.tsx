import "./globals.css";

export const metadata = {
  title: "study-space",
  description:
    "A website that encourages focus and motivation for producitvity using the pomodoro method",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex h-screen flex-col space-bg text-white">{children}</body>
    </html>
  );
}
