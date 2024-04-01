import { useState } from "react";
import {
  Table,
  Pagination,
  Group,
  Modal,
  Code,
  Button,
  TextInput,
  Container,
  Center,
  Title,
} from "@mantine/core";
import { useIoTData } from "@/hooks/useIoTData";
import { useDebouncedValue } from "@mantine/hooks";
import { formatDate } from "@/utils/utils";

const PAGE_SIZE = 10;

export default function IoTDataTablePage() {
  const [page, setPage] = useState(1);
  const [topicFilter, setTopicFilter] = useState("");
  const [debounced] = useDebouncedValue(topicFilter, 400);

  const { iotData, totalPages, isLoading, isError } = useIoTData(
    page,
    PAGE_SIZE,
    debounced,
  );

  // State to control the modal visibility and content
  const [isModalOpen, setModalOpen] = useState(false);
  const [selectedData, setSelectedData] = useState<any>(null);

  // Function to handle row click, setting the selected data and opening the modal
  const handleRowClick = (data: any) => {
    setSelectedData(data);
    setModalOpen(true);
  };

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error loading data</div>;

  return (
    <Container>
      <Title>IoT Data Logs</Title>
      <TextInput
        placeholder="Filter by topic"
        value={topicFilter}
        onChange={(e) => setTopicFilter(e.currentTarget.value)}
        my="md"
        mb={16}
      />
      <Table striped highlightOnHover>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Time</Table.Th>
            <Table.Th>Topic</Table.Th>
            <Table.Th>Location</Table.Th>
            <Table.Th>Data</Table.Th>
            <Table.Th>Unit</Table.Th>
            <Table.Th>Action</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <tbody>
          {iotData?.map((item) => (
            <Table.Tr key={item.id}>
              <Table.Td> {formatDate(item.time)}</Table.Td>
              <Table.Td>{item.topic}</Table.Td>
              <Table.Td>{item.location}</Table.Td>
              <Table.Td
                style={{
                  maxWidth: "200px",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
                title={JSON.stringify(item.data, null, 2)}
              >
                {JSON.stringify(item.data)}
              </Table.Td>
              <Table.Td>{item.unit}</Table.Td>
              <Table.Td>
                <Button size="xs" onClick={() => handleRowClick(item.data)}>
                  View Data
                </Button>
              </Table.Td>
            </Table.Tr>
          ))}
        </tbody>
      </Table>
      <Center mt={16}>
        <Pagination
          total={totalPages}
          page={page}
          onChange={(page) => setPage(page)}
        />
      </Center>
      <Modal
        opened={isModalOpen}
        onClose={() => setModalOpen(false)}
        title="Detailed Data"
        size="lg"
      >
        <Code block>{JSON.stringify(selectedData, null, 2)}</Code>
      </Modal>
    </Container>
  );
}
