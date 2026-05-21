import Footer from "@/components/Footer";
import ChatPopup from "@/components/ChatPopup";
import Planet from "@/components/Planet";

const Home = () => {
  return (
    <div className="flex min-h-[85vh] w-full flex-col items-center justify-start">

      <main className="mt-12 w-full max-w-5xl px-6 lg:px-0">
        <section id="welcome" className="py-24 text-center">
          <h1 className="text-5xl font-bold">Study Space</h1>
          <p className="mt-8 text-lg text-gray-200">
            An AI-powered study style quiz app that helps you discover how you learn best — and gives you personalized study strategies to match your learning style (coming soon).
          </p>
          <Planet />
          <ChatPopup />
        </section>

        <section id="pomodoro" className="py-12">
          {/* Pomodoro section removed per request */}
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default Home;
