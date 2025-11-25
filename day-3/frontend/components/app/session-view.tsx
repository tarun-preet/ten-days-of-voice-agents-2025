'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Bot, Globe, Mic, Video } from 'lucide-react';
import { type HTMLMotionProps, motion } from 'motion/react';
import type { AppConfig } from '@/app-config';
import { BentoCard, BentoGrid } from '@/components/app/bento-grid';
import { ChatTranscript } from '@/components/app/chat-transcript';
import { PreConnectMessage } from '@/components/app/preconnect-message';
import {
  AgentControlBar,
  type ControlBarControls,
} from '@/components/livekit/agent-control-bar/agent-control-bar';
import { useChatMessages } from '@/hooks/useChatMessages';
import { useConnectionTimeout } from '@/hooks/useConnectionTimout';
import { useDebugMode } from '@/hooks/useDebug';
import { cn } from '@/lib/utils';
import { ScrollArea } from '../livekit/scroll-area/scroll-area';
import { BorderBeam } from './border-beam';

const MotionBottom = motion.create('div');

const IN_DEVELOPMENT = process.env.NODE_ENV !== 'production';
const BOTTOM_VIEW_MOTION_PROPS: HTMLMotionProps<'div'> = {
  variants: {
    visible: {
      opacity: 1,
      translateY: '0%',
    },
    hidden: {
      opacity: 0,
      translateY: '100%',
    },
  },
  initial: 'hidden',
  animate: 'visible',
  exit: 'hidden',
  transition: {
    duration: 0.3,
    delay: 0.5,
    ease: [0, 0, 0.58, 1] as const,
  },
};

interface FadeProps {
  top?: boolean;
  bottom?: boolean;
  className?: string;
}

export function Fade({ top = false, bottom = false, className }: FadeProps) {
  return (
    <div
      className={cn(
        'from-background pointer-events-none h-4 bg-linear-to-b to-transparent',
        top && 'bg-linear-to-b',
        bottom && 'bg-linear-to-t',
        className
      )}
    />
  );
}
interface SessionViewProps {
  appConfig: AppConfig;
}

export const SessionView = ({
  appConfig,
  ...props
}: React.ComponentProps<'section'> & SessionViewProps) => {
  useConnectionTimeout(200_000);
  useDebugMode({ enabled: IN_DEVELOPMENT });

  const messages = useChatMessages();
  // Always show transcriptions for voice agents - chat toggle only controls text input
  const [, setChatOpen] = useState(true);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  const controls: ControlBarControls = {
    leave: true,
    microphone: true,
    chat: appConfig.supportsChatInput,
    camera: appConfig.supportsVideoInput,
    screenShare: appConfig.supportsVideoInput,
  };

  // Auto-scroll to bottom when new messages arrive (for all messages, not just local)
  useEffect(() => {
    if (scrollAreaRef.current && messages.length > 0) {
      // Use requestAnimationFrame to ensure DOM has updated
      requestAnimationFrame(() => {
        if (scrollAreaRef.current) {
          scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
        }
      });
    }
  }, [messages]);

  const features = [
    {
      Icon: Globe,
      name: 'Worldwide',
      description: 'Connect with anyone, anywhere in the world.',
      href: '/',
      cta: 'Learn more',
      className: 'col-span-3 lg:col-span-1',
      background: (
        <div className="absolute top-0 -z-10 h-full w-full bg-[url('/path-to-globe-image.png')] bg-cover bg-center" />
      ),
    },
    {
      Icon: Bot,
      name: 'AI-Powered',
      description: 'Experience the power of AI in your conversations.',
      href: '/',
      cta: 'Learn more',
      className: 'col-span-3 lg:col-span-2',
      background: (
        <div className="absolute top-0 -z-10 h-full w-full bg-gradient-to-r from-blue-500 to-purple-500 opacity-20" />
      ),
    },
    {
      Icon: Mic,
      name: 'Voice Control',
      description: 'Control the session with your voice.',
      href: '/',
      cta: 'Learn more',
      className: 'col-span-3 lg:col-span-2',
      background: (
        <div className="absolute top-0 -z-10 h-full w-full bg-gradient-to-r from-green-500 to-teal-500 opacity-20" />
      ),
    },
    {
      Icon: Video,
      name: 'Video Conferencing',
      description: 'High-quality video conferencing for seamless communication.',
      href: '/',
      cta: 'Learn more',
      className: 'col-span-3 lg:col-span-1',
      background: (
        <div className="absolute top-0 -z-10 h-full w-full bg-gradient-to-r from-yellow-500 to-orange-500 opacity-20" />
      ),
    },
  ];

  return (
    <section className="bg-background relative z-10 h-full w-full overflow-hidden" {...props}>
      <div className="pointer-events-none fixed inset-0 z-[60] grid grid-cols-1 grid-rows-1">
        <Fade top className="pointer-events-none absolute inset-x-4 top-0 h-40" />
        <ScrollArea
          ref={scrollAreaRef}
          className="pointer-events-auto px-4 pt-40 pb-[150px] md:px-6 md:pb-[180px]"
        >
          <ChatTranscript
            hidden={false}
            messages={messages}
            className="mx-auto max-w-2xl space-y-3"
          />
        </ScrollArea>
      </div>

      <BentoGrid className="absolute inset-0 m-4 lg:grid-rows-3">
        {features.map(({ Icon, name, description, className, background }, index) => (
          <BentoCard
            key={name}
            className={cn(
              'relative flex flex-col justify-between overflow-hidden rounded-xl',
              'transform-gpu bg-transparent [box-shadow:0_-20px_80px_-20px_#ffffff1f_inset] [border:1px_solid_rgba(255,255,255,.1)]',
              className
            )}
          >
            {background}
            <div className="pointer-events-none z-10 flex transform-gpu flex-col gap-1 p-6 transition-all duration-300">
              <Icon className="h-12 w-12 origin-left transform-gpu text-neutral-700 transition-all duration-300 ease-in-out group-hover:scale-75" />
              <h3 className="text-xl font-semibold text-neutral-700 dark:text-neutral-300">
                {name}
              </h3>
              <p className="max-w-lg text-neutral-400">{description}</p>
            </div>
            {index === 0 && <BorderBeam />}
          </BentoCard>
        ))}
      </BentoGrid>

      <MotionBottom
        {...BOTTOM_VIEW_MOTION_PROPS}
        className="fixed inset-x-3 bottom-0 z-[70] md:inset-x-12"
      >
        {appConfig.isPreConnectBufferEnabled && (
          <PreConnectMessage messages={messages} className="pb-4" />
        )}
        <div className="bg-background relative mx-auto max-w-2xl pb-3 md:pb-12">
          <Fade bottom className="absolute inset-x-0 top-0 h-4 -translate-y-full" />
          <AgentControlBar controls={controls} onChatOpenChange={setChatOpen} />
        </div>
      </MotionBottom>
    </section>
  );
};
