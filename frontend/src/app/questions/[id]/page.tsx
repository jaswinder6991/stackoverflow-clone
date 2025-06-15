import QuestionDetail from "@/components/QuestionDetail";
import Layout from "@/components/Layout";

interface QuestionPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function QuestionPage({ params }: QuestionPageProps) {
  const { id } = await params;
  
  return (
    <Layout>
      <div className="bg-white min-h-screen">
        <QuestionDetail questionId={parseInt(id)} />
      </div>
    </Layout>
  );
}
