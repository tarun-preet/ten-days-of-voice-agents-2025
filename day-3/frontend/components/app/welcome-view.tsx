import { Bot } from 'lucide-react';
// Decorative images removed per user request
import { Button } from '@/components/livekit/button';

function WelcomeImage() {
  return (
    <div className="welcome-bot bot-bounce mb-4">
      <Bot size={36} className="text-black" />
    </div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref} className="px-6 py-12">
      <section className="therapist-card text-center">
        <WelcomeImage />

        <h1
          className="text-card-foreground mb-2 text-2xl font-semibold"
          style={{ color: '#000000' }}
        >
          Welcome to Your Safe Space
        </h1>
        <p
          className="subtitle text-card-foreground mx-auto max-w-prose pt-1 leading-6 font-medium"
          style={{ color: '#000000' }}
        >
          A calm, confidential place to explore your thoughts. When you are ready, we can start a
          chat.
        </p>

        <div className="mt-6">
          <Button
            variant="primary"
            size="lg"
            onClick={onStartCall}
            className="button-glow w-64 font-mono shadow-md"
          >
            {startButtonText}
          </Button>
        </div>

        <div className="muted-box mt-6">
          <p className="text-muted-foreground/90 text-sm">
            Tip: Try taking a deep breath before starting — you can share as much or as little as
            you like.
          </p>
        </div>
        {/* Decorative images removed */}
      </section>
    </div>
  );
};
