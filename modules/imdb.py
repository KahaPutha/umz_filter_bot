from imdb import IMDb
from telegram import Update
from telegram.ext import ContextTypes

# Initialize the IMDb object
ia = IMDb()

async def imdb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch IMDb information about a movie based on the title."""
    if context.args:
        # Get the movie title from the command arguments
        movie_title = ' '.join(context.args)

        try:
            # Search for the movie
            movies = ia.search_movie(movie_title)
            if not movies:
                await update.message.reply_text(f"❌ No results found for '{movie_title}'. Please try again.")
                return

            # Get the first movie in the search results
            movie = movies[0]

            # Get detailed information about the movie
            ia.update(movie)

            # Collect details to show, with fallbacks for missing info
            title = movie.get('title', "Unknown Title")
            year = movie.get('year', "Unknown Year")
            plot = movie.get('plot', ["No plot available"])[0]
            rating = movie.get('rating', "No rating available")
            genres = ", ".join(movie.get('genres', [])) or "No genres available"
            director = movie.get('directors', ["Unknown"])[0] if movie.get('directors') else "Unknown"
            poster_url = movie.get('full-size cover url', "https://via.placeholder.com/200x300?text=No+Poster+Available")

            # Prepare the response text with proper formatting
            response_text = f"🎬 **{title}** ({year})\n"
            response_text += f"⭐ **Rating**: {rating}/10\n"
            response_text += f"🎥 **Genres**: {genres}\n"
            response_text += f"🎬 **Director**: {director}\n"
            response_text += f"📜 **Plot**: {plot}\n"

            # Send the movie details to the user
            await update.message.reply_photo(
                photo=poster_url,
                caption=response_text
            )

        except Exception as e:
            # Specific error message for IMDb API failures or other exceptions
            await update.message.reply_text(f"❌ Error fetching movie details: {str(e)}")

    else:
        # Provide usage instructions if no movie title is given
        await update.message.reply_text("❌ Please provide a movie title after the command. Example: /imdb The Matrix")
