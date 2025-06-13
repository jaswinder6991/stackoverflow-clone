import QuestionDetail from "@/components/QuestionDetail";
import { generateSampleQuestion } from "@/lib/sampleData";

interface QuestionPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function QuestionPage({ params }: QuestionPageProps) {
  const { id } = await params;
  
  // Generate sample question data based on ID
  const questionData = generateSampleQuestion(parseInt(id));

  return (
    <div className="bg-white min-h-screen">
      <QuestionDetail question={questionData} />
    </div>
  );
}
