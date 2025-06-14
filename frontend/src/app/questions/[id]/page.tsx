import QuestionDetail from "@/components/QuestionDetail";

interface QuestionPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function QuestionPage({ params }: QuestionPageProps) {
  const { id } = await params;
  
  return (
    <div className="bg-white min-h-screen">
      <QuestionDetail questionId={parseInt(id)} />
    </div>
  );
}
