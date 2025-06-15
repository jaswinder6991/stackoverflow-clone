import QuestionDetail from "@/components/QuestionDetail";
import Layout from "@/components/Layout";

interface QuestionPageProps {
  params: Promise<{
    id: string;
    slug: string;
  }>;
}

export default async function QuestionDetailPage({ params }: QuestionPageProps) {
  const { id } = await params;
  // Note: slug parameter is available for SEO but not used in this implementation
  
  return (
    <Layout>
    <div className="bg-white min-h-screen">
      <QuestionDetail questionId={parseInt(id)} />
    </div>
    </Layout>
  );
}
