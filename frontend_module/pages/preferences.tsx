import { PreferenceDTO } from "@/constants/interfaces";
import { usePreferences } from "@/hooks/usePreferences";
import {
  Box,
  Button,
  Card,
  Center,
  Container,
  Flex,
  Group,
  Modal,
  Pagination,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { useEffect, useState } from "react";
import { useSWRConfig } from "swr";
import dynamic from "next/dynamic";
import PreferenceModal from "@/components/PreferenceModal";
import { formatDate } from "@/utils/utils";

export default function PreferencesPage() {
  const [isClient, setIsClient] = useState(false);
  const [apiUrl, setApiUrl] = useState<string>("");

  useEffect(() => {
    // This code runs only in the browser, where `window` is defined
    const baseURL =
      process.env.REACT_APP_API_URL ||
      window.location.origin.replace(":3000", ":5000");
    setApiUrl(baseURL);
  }, []);

  const { mutate } = useSWRConfig();
  const [currentPage, setCurrentPage] = useState(1);

  const { preferences, totalPages, isLoading, isError } =
    usePreferences(currentPage);

  // Modal state
  const [isModalOpen, setModalOpen] = useState(false);
  const [currentPreference, setCurrentPreference] = useState(null);

  const handlePageChange = (page: number) => setCurrentPage(page);

  const handleSave = async (values: any) => {
    const url =
      apiUrl +
      "/preferences" +
      (currentPreference ? `/${currentPreference.id}` : "/");
    const method = currentPreference ? "PUT" : "POST";
    values.updatedBy = "User";
    try {
      const response = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });

      if (!response.ok) throw new Error("Network response was not ok");

      setModalOpen(false); // Close the modal
      mutate(`${apiUrl}/preferences?page=${currentPage}&size=10`);
      // Optionally, fetch preferences again or update local state to reflect the change
    } catch (error) {
      console.error("There was a problem with your fetch operation:", error);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this preference?")) return;

    try {
      const response = await fetch(`${apiUrl}/preferences/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error("Network response was not ok");

      mutate(`${apiUrl}/preferences?page=${currentPage}&size=10`);
    } catch (error) {
      console.error("There was a problem with your fetch operation:", error);
    }
  };

  // When adding a new preference
  const openAddModal = () => {
    setCurrentPreference(null); // Ensure no previous data is loaded
    setModalOpen(true);
  };

  // When editing an existing preference
  const openEditModal = (preference: any) => {
    setCurrentPreference(preference);
    setModalOpen(true);
  };

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching preferences.</div>;

  return (
    <Container>
      <Stack>
        <Flex justify="space-between" mb={20}>
          <Title>Preferences</Title>
          <Button style={{ float: "right" }} onClick={openAddModal}>
            Add Preference
          </Button>
        </Flex>
        {preferences &&
          preferences.map((pref) => (
            <Card key={pref.id} shadow="sm" padding="lg" radius="md" withBorder>
              <div>
                <Text>{pref.description}</Text>
                <Text size="sm" mt={8}>
                  Last Updated: {formatDate(pref.updatedAt || pref.createdAt)}{" "}
                  by {pref.updatedBy}
                </Text>
              </div>
              <Group mt={16}>
                <Button onClick={() => openEditModal(pref)}>Edit</Button>
                <Button color="red" onClick={() => handleDelete(pref.id)}>
                  Delete
                </Button>
              </Group>
            </Card>
          ))}
        <Center>
          <Pagination
            value={currentPage}
            onChange={handlePageChange}
            total={totalPages || 0}
            style={{ marginTop: 20 }}
          />
        </Center>
        <PreferenceModal
          opened={isModalOpen}
          setOpened={setModalOpen}
          onSave={handleSave}
          initialData={currentPreference}
        />
      </Stack>
    </Container>
  );
}
