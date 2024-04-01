import "@mantine/core/styles.css";
import type { AppProps } from "next/app";
import Head from "next/head";
import {
  ActionIcon,
  Flex,
  Group,
  MantineProvider,
  NavLink,
  Text,
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
import { usePathname } from "next/navigation";

export const ROUTES = [
  { path: "/", label: "Home", icon: <IconHome2 /> },
  { path: "/preferences", label: "Preferences", icon: <IconUserCircle /> },
  { path: "/chatlogs", label: "Chat Logs", icon: <IconMessageDots /> },
];

export default function App({ Component, pageProps }: AppProps) {
  const [opened, { toggle }] = useDisclosure();
  const router = useRouter();
  const pathname = usePathname();

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
              <Title>
                <Text
                  inherit
                  variant="gradient"
                  gradient={{ from: "blue", to: "green" }}
                >
                  Mirai
                </Text>
              </Title>
            </Link>
            <ColorSchemeToggle />
          </Flex>
        </AppShell.Header>

        <AppShell.Navbar p="lg">
          {ROUTES.map(({ path, label, icon }) => (
            <NavLink
              key={path}
              onClick={() => router.push(path)}
              label={label}
              leftSection={icon}
              active={pathname === path}
            />
          ))}
        </AppShell.Navbar>

        <AppShell.Main>
          <Component {...pageProps} />
        </AppShell.Main>
      </AppShell>
    </MantineProvider>
  );
}
