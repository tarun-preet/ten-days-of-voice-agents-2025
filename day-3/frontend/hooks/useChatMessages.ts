import { useMemo } from 'react';
import { Room } from 'livekit-client';
import {
  type ReceivedChatMessage,
  type TextStreamData,
  useChat,
  useRoomContext,
  useTranscriptions,
} from '@livekit/components-react';

function transcriptionToChatMessage(textStream: TextStreamData, room: Room): ReceivedChatMessage {
  // Use stream ID which should handle both interim and final transcriptions
  // Interim transcriptions will update the same message as they arrive
  return {
    id: textStream.streamInfo.id,
    timestamp: textStream.streamInfo.timestamp,
    type: 'chatMessage',
    message: textStream.text,
    from:
      textStream.participantInfo.identity === room.localParticipant.identity
        ? room.localParticipant
        : Array.from(room.remoteParticipants.values()).find(
            (p) => p.identity === textStream.participantInfo.identity
          ),
  };
}

export function useChatMessages() {
  const chat = useChat();
  const room = useRoomContext();
  const transcriptions: TextStreamData[] = useTranscriptions();

  const mergedTranscriptions = useMemo(() => {
    // Show all transcriptions including interim updates for real-time display
    const merged: Array<ReceivedChatMessage> = [
      ...transcriptions.map((transcription) => transcriptionToChatMessage(transcription, room)),
      ...chat.chatMessages,
    ];
    // Sort by timestamp to show messages in order
    // For interim updates with same segment_id, the latest will be at the end
    return merged.sort((a, b) => {
      // If timestamps are equal, prefer later messages (likely interim updates)
      if (a.timestamp === b.timestamp) {
        return a.id > b.id ? 1 : -1;
      }
      return a.timestamp - b.timestamp;
    });
  }, [transcriptions, chat.chatMessages, room]);

  return mergedTranscriptions;
}
