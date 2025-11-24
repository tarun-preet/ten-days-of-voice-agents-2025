import { Button } from '@/components/livekit/button';

function WelcomeImage() {
  return (
    <svg
      width="128"
      height="128"
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="text-fg0 mb-4 size-32"
    >
      <path
        d="M12 16C12 13.7909 13.7909 12 16 12H40C42.2091 12 44 13.7909 44 16V42C44 44.2091 42.2091 46 40 46H16C13.7909 46 12 44.2091 12 42V16Z M44 22C48.4183 22 52 25.5817 52 30C52 34.4183 48.4183 38 44 38V40C49.5228 40 54 35.5228 54 30C54 24.4772 49.5228 20 44 20V22Z M21 6C21 4.89543 21.8954 4 23 4C24.1046 4 25 4.89543 25 6V10C25 11.1046 24.1046 12 23 12C21.8954 12 21 11.1046 21 10V6Z M29 8C29 6.89543 29.8954 6 31 6C32.1046 6 33 6.89543 33 8V12C33 13.1046 32.1046 14 31 14C29.8954 14 29 13.1046 29 12V8Z"
        fill="currentColor"
      />
    </svg>
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
    <div ref={ref}>
      <section className="bg-background flex flex-col items-center justify-center text-center">
        <WelcomeImage />

        <p className="text-foreground max-w-prose pt-1 leading-6 font-medium">
          Chat live with your Barista
        </p>

        <Button variant="primary" size="lg" onClick={onStartCall} className="mt-6 w-64 font-mono">
          {startButtonText}
        </Button>
      </section>
    </div>
  );
};
