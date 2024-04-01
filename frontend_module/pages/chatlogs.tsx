import { useState } from "react";
import {
  Container,
  Group,
  Text,
  Button,
  Avatar,
  Center,
  ActionIcon,
  Stack,
  Box,
  Pill,
  Badge,
  Flex,
  Title,
} from "@mantine/core";
import { useChatLogs } from "../hooks/useChatLogs"; // Adjust the import path as necessary
import {
  IconChevronLeft,
  IconChevronRight,
  IconChevronsLeft,
  IconChevronsRight,
} from "@tabler/icons-react";
import { formatDate } from "@/utils/utils";

const ChatLogsPage: React.FC = () => {
  const [page, setPage] = useState(1);
  const { chatlog, totalPages, isLoading, isError } = useChatLogs(page);

  if (isError) return <div>Failed to load</div>;
  if (isLoading) return <div>Loading...</div>;

  const nextPage = () => {
    if (page < totalPages) setPage(page + 1);
  };

  const prevPage = () => {
    if (page > 1) setPage(page - 1);
  };

  const getAIMessage = (log) => {
    return (
      <Flex key={log.id}>
        <Avatar color="cyan" radius="xl" mx={16}>
          AI
        </Avatar>
        <Box bg="cyan" p={8} style={{ borderRadius: "5px" }}>
          <Stack>
            <Text size="sm">{formatDate(log.time)}</Text>
            <Text>{log.message}</Text>{" "}
          </Stack>{" "}
        </Box>
      </Flex>
    );
  };

  const getUserMessage = (log) => {
    return (
      <Flex key={log.id} justify="flex-end">
        <Box bg="green" p={8} style={{ borderRadius: "5px" }}>
          <Stack>
            <Text size="sm">{formatDate(log.time)}</Text>
            <Text>{log.message}</Text>{" "}
          </Stack>{" "}
        </Box>
        <Avatar color="green" radius="xl" mx={16}>
          You
        </Avatar>
      </Flex>
    );
  };

  return (
    <Container>
      <Title>Chat Logs</Title>
      <Stack mt={20}>
        {chatlog?.map((log) =>
          log.sentBy === "assistant" ? getAIMessage(log) : getUserMessage(log),
        )}
      </Stack>
      <Center>
        <Group mt="md">
          <ActionIcon onClick={prevPage} disabled={page <= 1}>
            <IconChevronsLeft />
          </ActionIcon>
          <ActionIcon onClick={nextPage} disabled={page >= totalPages}>
            <IconChevronsRight />
          </ActionIcon>
        </Group>
      </Center>
    </Container>
  );
};

export default ChatLogsPage;
