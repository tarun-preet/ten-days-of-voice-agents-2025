'use client';

import { AnimatePresence, type HTMLMotionProps, motion } from 'motion/react';
import { type ReceivedChatMessage } from '@livekit/components-react';
import { ChatEntry } from '@/components/livekit/chat-entry';

const MotionContainer = motion.create('div');
const MotionChatEntry = motion.create(ChatEntry);

const CONTAINER_MOTION_PROPS = {
  variants: {
    hidden: {
      opacity: 0,
      transition: {
        // Use a cubic-bezier easing array instead of a string to satisfy typing
        ease: [0.25, 0.1, 0.25, 1],
        duration: 0.3,
        staggerChildren: 0.1,
        staggerDirection: -1,
      },
    },
    visible: {
      opacity: 1,
      transition: {
        delay: 0.2,
        ease: [0.25, 0.1, 0.25, 1],
        duration: 0.3,
        // 'stagerDelay' looked like a typo; it should be 'delay' / 'delayChildren'.
        delayChildren: 0.2,
        staggerChildren: 0.1,
        staggerDirection: 1,
      },
    },
  },
  initial: 'hidden',
  animate: 'visible',
  exit: 'hidden',
} as const;

const MESSAGE_MOTION_PROPS = {
  variants: {
    hidden: {
      opacity: 0,
      translateY: 10,
    },
    visible: {
      opacity: 1,
      translateY: 0,
    },
  },
} as const;

interface ChatTranscriptProps {
  hidden?: boolean;
  messages?: ReceivedChatMessage[];
}

export function ChatTranscript({
  hidden = false,
  messages = [],
  ...props
}: ChatTranscriptProps & Omit<HTMLMotionProps<'div'>, 'ref'>) {
  // If not hidden, start visible immediately for voice agents
  if (!hidden) {
    return (
      <MotionContainer {...props} style={{ opacity: 1 }}>
        {messages.map(({ id, timestamp, from, message, editTimestamp }: ReceivedChatMessage) => {
          const locale = navigator?.language ?? 'en-US';
          const messageOrigin = from?.isLocal ? 'local' : 'remote';
          const hasBeenEdited = !!editTimestamp;

          return (
            <ChatEntry
              key={id}
              locale={locale}
              timestamp={timestamp}
              message={message}
              messageOrigin={messageOrigin}
              hasBeenEdited={hasBeenEdited}
            />
          );
        })}
      </MotionContainer>
    );
  }

  // Hidden state with animations
  return (
    <AnimatePresence>
      <MotionContainer {...CONTAINER_MOTION_PROPS} {...props}>
        {messages.map(({ id, timestamp, from, message, editTimestamp }: ReceivedChatMessage) => {
          const locale = navigator?.language ?? 'en-US';
          const messageOrigin = from?.isLocal ? 'local' : 'remote';
          const hasBeenEdited = !!editTimestamp;

          return (
            <MotionChatEntry
              key={id}
              locale={locale}
              timestamp={timestamp}
              message={message}
              messageOrigin={messageOrigin}
              hasBeenEdited={hasBeenEdited}
              {...MESSAGE_MOTION_PROPS}
            />
          );
        })}
      </MotionContainer>
    </AnimatePresence>
  );
}
