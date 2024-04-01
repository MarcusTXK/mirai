import { Modal, Button, TextInput, Group } from "@mantine/core";
import { useForm } from "@mantine/form";
import { useEffect, useState } from "react";

export default function PreferenceModal({
  opened,
  setOpened,
  onSave,
  initialData,
}) {
  const form = useForm({
    initialValues: {
      description: "",
      updatedBy: "User", // This will be overridden by ...initialData when editing
    },
  });

  // Effect to re-initialize form when initialData changes
  useEffect(() => {
    if (initialData) {
      form.setValues({
        description: initialData.description,
        updatedBy: "User", // Ensuring 'updatedBy' is always set to "User" on edit
      });
    } else {
      form.reset(); // Reset the form to initial values if there's no initialData
    }
  }, [initialData]);

  return (
    <Modal
      opened={opened}
      onClose={() => {
        setOpened(false);
        form.reset();
      }}
      title={initialData ? "Edit Preference" : "Add Preference"}
    >
      <form onSubmit={form.onSubmit((values) => onSave(values))}>
        <TextInput
          required
          withAsterisk
          label="Description"
          placeholder="Preference description"
          {...form.getInputProps("description")}
        />
        <Group mt="md">
          <Button type="submit">Save</Button>
        </Group>
      </form>
    </Modal>
  );
}
