import "@mantine/core/styles.css";
import type { AppProps } from "next/app";
import Head from "next/head";
import {
  ActionIcon,
  Flex,
  Group,
  MantineProvider,
  NavLink,
  Title,
  useMantineColorScheme,
} from "@mantine/core";
import { theme } from "../theme";
import { AppShell, Burger } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import {
  IconHome2,
  IconMessageDots,
  IconUserCircle,
} from "@tabler/icons-react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ColorSchemeToggle } from "@/components/ColorSchemeToggle/ColorSchemeToggle";

export default function App({ Component, pageProps }: AppProps) {
  const [opened, { toggle }] = useDisclosure();
  const router = useRouter();

  return (
    <MantineProvider theme={theme}>
      <Head>
        <title>Mantine Template</title>
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
        <link rel="shortcut icon" href="/favicon.svg" />
      </Head>
      <AppShell
        header={{ height: 60 }}
        navbar={{
          width: 300,
          breakpoint: "sm",
          collapsed: { mobile: !opened },
        }}
        padding="md"
      >
        <AppShell.Header>
          <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
          <Flex
            h="100%"
            align="center"
            justify="space-between"
            w="100%"
            px="md"
          >
            <Link
              href={"/"}
              style={{ textDecoration: "none", color: "inherit" }}
            >
              <Title>Mirai</Title>
            </Link>
            <ColorSchemeToggle />
          </Flex>
        </AppShell.Header>

        <AppShell.Navbar p="lg">
          <NavLink
            onClick={() => router.push("/")}
            label="Home"
            leftSection={<IconHome2 />}
          />
          <NavLink
            onClick={() => router.push("/preferences")}
            label="Preferences"
            leftSection={<IconUserCircle />}
          />
          <NavLink
            onClick={() => router.push("/chatlogs")}
            label="Chat Logs"
            leftSection={<IconMessageDots />}
          />
        </AppShell.Navbar>

        <AppShell.Main>
          <Component {...pageProps} />
        </AppShell.Main>
      </AppShell>
    </MantineProvider>
  );
}
