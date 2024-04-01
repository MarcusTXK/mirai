import { ActionIcon, Group, useMantineColorScheme } from "@mantine/core";
import { IconSun, IconMoonStars } from "@tabler/icons-react";
import { useEffect, useState } from "react";

export function ColorSchemeToggle() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  const isDarkMode = colorScheme === "dark";

  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  return isClient ? (
    <Group>
      <ActionIcon
        size="lg"
        variant="default"
        onClick={toggleColorScheme}
        title={isDarkMode ? "Light mode" : "Dark mode"}
      >
        {isDarkMode ? <IconSun /> : <IconMoonStars />}
      </ActionIcon>
    </Group>
  ) : (
    <></>
  );
}
