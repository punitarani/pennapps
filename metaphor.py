from flask import Flask, request, jsonify
from metaphor_python import Metaphor

app = Flask(__name__)

metaphor_api = Metaphor(api_key='68288111-fc19-4a4e-b09f-396461d34387')

@app.route('/chat', methods=['POST'])
def chat():
    try:

        user_input = request.json.get('user_input')

        search_response = metaphor_api.search(
            query=user_input,
            num_results=5,
        )


        results = search_response.results

        response = {'bot_response': results}

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
