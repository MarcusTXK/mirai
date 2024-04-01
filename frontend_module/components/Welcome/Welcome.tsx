import { Title, Text, Anchor } from "@mantine/core";
import classes from "./Welcome.module.css";

export function Welcome() {
  return (
    <>
      <Title className={classes.title} ta="center" mt={100}>
        Welcome to{" "}
        <Text
          inherit
          variant="gradient"
          component="span"
          gradient={{ from: "blue", to: "green" }}
        >
          Mirai
        </Text>{" "}
        Dashboard
      </Title>
      <Text color="dimmed" ta="center" size="lg" maw={580} mx="auto" mt="xl">
        Mirai is an Open Source Local LLM Voice activated Home Assistant. For
        help with config refer to{" "}
        <Anchor href="https://github.com/MarcusTXK/mirai" size="lg">
          this guide
        </Anchor>
        . <br />
        <br />
        To get started with configuration, click on the navbar on the left.
      </Text>
    </>
  );
}
