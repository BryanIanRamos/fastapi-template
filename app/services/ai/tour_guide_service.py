"""
Tour Guide Service - Generates AI-powered tour guide responses using LLM
Uses LangChain with ChatOllama (or other LLM providers)
"""

from typing import List, Dict, Any, Optional
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.chat_models import ChatOllama
from app.core.config import settings


class TourGuideService:
    """Service for generating intelligent tour guide responses"""

    def __init__(
        self,
        llm_model: str = settings.OLLAMA_MODEL,
        llm_temperature: float = settings.OLLAMA_TEMPERATURE,
        llm_base_url: str = settings.OLLAMA_BASE_URL,
    ):
        """
        Initialize tour guide service
        
        Args:
            llm_model: Ollama model name (e.g., "gemma2", "mistral", "neural-chat")
            llm_temperature: Temperature for LLM responses (0-1, lower = more focused)
            llm_base_url: Base URL for Ollama server
        """
        self.model_name = llm_model
        self.temperature = llm_temperature
        self.base_url = llm_base_url
        self.llm = ChatOllama(
            model=llm_model,
            temperature=llm_temperature,
            base_url=llm_base_url,
        )

    def build_response(
        self,
        query: str,
        search_results: List[Dict[str, Any]],
        max_suggestions: int = 3,
        include_all: bool = False,
        min_similarity: Optional[float] = 0.4,
        require_relevance: bool = False,
    ) -> str:
        """
        Build a natural language response from search results
        
        Args:
            query: Original user query
            search_results: List of matching tourist areas from vector search
            max_suggestions: Maximum number of areas to include in response
            include_all: If True, include all results regardless of max_suggestions
            min_similarity: Minimum similarity threshold for filtering results
            require_relevance: If True, reject if no results meet min_similarity
            
        Returns:
            Natural language tour guide response
        """
        # Handle empty results
        if not search_results:
            return (
                "Sorry, I don't have enough information to answer that yet. "
                "Try asking about beaches, mountains, cultural sites, or activities."
            )

        # Select results to include
        if include_all:
            selected_results = search_results
        else:
            selected_results = search_results[:max_suggestions]

        if not selected_results:
            return "No relevant matches found in the retrieved data."

        # Filter by similarity threshold if provided
        filtered_results = []
        if min_similarity is not None:
            for result in selected_results:
                similarity = result.get("similarity_score", 0)
                if similarity >= min_similarity:
                    filtered_results.append(result)
        else:
            filtered_results = selected_results

        # Check relevance requirement
        if require_relevance and not filtered_results:
            return (
                "I could not find a strong enough match for that question. "
                "Try rephrasing or asking about another place or activity."
            )

        # Use filtered results if available, otherwise use selected
        final_results = filtered_results if filtered_results else selected_results

        # Build context from results
        context_lines = self._build_context_lines(final_results)
        context_block = "\n".join(context_lines)

        # Generate response using LLM
        response = self._invoke_llm(query, context_block)

        return response

    def _build_context_lines(self, results: List[Dict[str, Any]]) -> List[str]:
        """
        Build formatted context lines from search results
        
        Args:
            results: List of search results
            
        Returns:
            List of formatted context strings
        """
        context_lines = []

        for result in results:
            area_id = result.get("area_id")
            name = result.get("name", "Unknown")
            description = result.get("description", "")
            location = result.get("location", "Unknown")
            region = result.get("region", "")
            category = result.get("category", "")
            latitude = result.get("latitude")
            longitude = result.get("longitude")
            avg_rating = result.get("avg_rating")
            visit_count = result.get("visit_count", 0)
            content = result.get("content", "")
            similarity = result.get("similarity_score", 0)

            # Format coordinates
            coords_str = ""
            if latitude and longitude:
                coords_str = f" | GPS: ({latitude:.4f}, {longitude:.4f})"

            # Format rating and popularity
            popularity_str = ""
            if avg_rating:
                popularity_str += f" | Rating: ⭐ {avg_rating:.1f}"
            if visit_count:
                popularity_str += f" | Visits: {visit_count}"

            # Format activities
            activities = result.get("activities", [])
            activity_str = ""
            if activities:
                activity_names = [a.get("activity_name", "") for a in activities[:3]]
                activity_str = f" | Activities: {', '.join(activity_names)}"

            # Format reviews
            reviews = result.get("reviews", [])
            review_str = ""
            if reviews:
                top_review = reviews[0]
                user = top_review.get("user_name", "Traveler")
                rating = top_review.get("rating", 0)
                comment = top_review.get("comment", "")[:80]
                review_str = f" | Review: {user} gave ⭐ {rating}: \"{comment}\""

            # Build complete line
            region_info = f" in {region}" if region else ""
            desc_preview = f": {description[:80]}..." if description else ""
            match_score = f" [Match: {similarity:.1%}]" if similarity else ""

            context_line = (
                f"🏛️ {name}{region_info}{coords_str}"
                f" | Category: {category}"
                f"{desc_preview}"
                f"{activity_str}"
                f"{review_str}"
                f"{popularity_str}"
                f"{match_score}"
            )

            context_lines.append(context_line)

        return context_lines

    def _invoke_llm(self, query: str, context_block: str) -> str:
        """
        Invoke the LLM to generate a response
        
        Args:
            query: User query
            context_block: Formatted context from search results
            
        Returns:
            LLM-generated response
        """
        system_prompt = (
            "You are a knowledgeable and friendly tour guide AI assistant. "
            "Your role is to help travelers discover amazing tourist destinations and activities. "
            "Instructions:\n"
            "- Only use information from the provided tourist data\n"
            "- Do NOT invent or guess new places or details\n"
            "- Consider user reviews, ratings, and popularity in your recommendations\n"
            "- If data partially answers the question, mention what is available\n"
            "- Keep responses concise and well-organized\n"
            "- Use bullet points for lists to make it easy to read\n"
            "- Include practical information: ratings, prices, difficulty levels, duration\n"
            "- Be enthusiastic but informative\n"
            "- If the match isn't perfect, ask a brief clarifying follow-up question"
        )

        user_message = (
            f"User Question: {query}\n\n"
            f"Available Tourist Destinations:\n"
            f"{context_block}\n\n"
            f"Please provide a helpful recommendation based on the above information. "
            f"Format your response clearly with bullet points where appropriate. "
            f"Include key details like pricing, activities, and user ratings."
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            print(f"Error invoking LLM: {e}")
            return f"I encountered an issue generating a response. Please try again."

    def generate_itinerary(
        self,
        search_results: List[Dict[str, Any]],
        duration_days: int = 3,
        interests: List[str] = None,
    ) -> str:
        """
        Generate a multi-day itinerary from search results
        
        Args:
            search_results: List of tourist areas
            duration_days: Number of days for the itinerary
            interests: List of interests (e.g., ["adventure", "culture", "food"])
            
        Returns:
            Formatted itinerary string
        """
        if not search_results:
            return "No destinations available to create an itinerary."

        interests_str = ", ".join(interests) if interests else "general tourism"

        # Build context
        context_lines = self._build_context_lines(search_results)
        context_block = "\n".join(context_lines)

        system_prompt = (
            "You are an expert travel planner. Create a detailed, realistic itinerary "
            "based on the provided destinations. Consider travel time, activities, and rest."
        )

        user_message = (
            f"Create a {duration_days}-day itinerary for travelers interested in {interests_str}.\n\n"
            f"Available Destinations:\n"
            f"{context_block}\n\n"
            f"Please create a day-by-day itinerary with specific destinations, activities, and timing."
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            print(f"Error generating itinerary: {e}")
            return "Could not generate itinerary at this time."

    def get_budget_recommendation(
        self,
        search_results: List[Dict[str, Any]],
        budget: float,
    ) -> str:
        """
        Get budget-friendly recommendations from search results
        
        Args:
            search_results: List of tourist areas
            budget: Budget in local currency
            
        Returns:
            Formatted recommendation string
        """
        if not search_results:
            return "No destinations available within your budget."

        context_lines = self._build_context_lines(search_results)
        context_block = "\n".join(context_lines)

        system_prompt = (
            "You are a budget travel advisor. Recommend destinations and activities "
            "that fit within the specified budget. Be practical and honest about costs."
        )

        user_message = (
            f"I have a budget of {budget}. What are the best destinations and activities I can enjoy?\n\n"
            f"Available Destinations:\n"
            f"{context_block}\n\n"
            f"Please recommend destinations and activities that fit this budget, and explain the costs."
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            print(f"Error generating budget recommendation: {e}")
            return "Could not generate budget recommendation at this time."
