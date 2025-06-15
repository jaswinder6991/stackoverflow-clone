import TopNav from "@/components/TopNav";

export default function UsersLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div>
      <TopNav />
      <main>{children}</main>
    </div>
  );
} 