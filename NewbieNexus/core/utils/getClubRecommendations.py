from core.models import Club,User
from core.serializers import ClubSerializer,UserSerializer



def getClubRecommendations(user):

    club_objects=Club.objects.all()
    serializer=ClubSerializer(club_objects,many=True)
    club_data={}
    for club in serializer.data:
        club_data[club["id"]]={
            "Interests":[],
            "Weights":[]
        }
        for interest in club["interests"]:
            club_data[club["id"]]["Interests"].append(interest["name"])
            club_data[club["id"]]["Weights"].append(interest["weight"])

    user_object=User.objects.get(id=user)
    serializer=UserSerializer(user_object)
    user_interests=[]
    user_weights=[]
    recommended_clubs=[]
    for interest in serializer.data["interests"]:
        user_interests.append(interest["name"])
        user_weights.append(interest["weight"])
    

    for club,club_info in club_data.items():
        club_interests = club_info["Interests"]
        club_weights = club_info["Weights"]

    # Calculate the similarity based on user interests and weights
        common_interests = set(user_interests).intersection(club_interests)
        similarity_score = 0
        for interest in common_interests:
            user_weight = user_weights[user_interests.index(interest)]
            club_weight = club_weights[club_interests.index(interest)]
            similarity_score += user_weight * club_weight
        
    #similarity_scores.append((club, similarity_score))

    # Exclude clubs with a similarity score of zero or below
        if similarity_score > 5:
            recommended_clubs.append((club, similarity_score))

    club_ids=[obj[0] for obj in recommended_clubs]

    clubs=Club.objects.filter(id__in=club_ids)
    serializer=ClubSerializer(clubs,many=True)
    sorted_recommended_clubs = sorted(recommended_clubs, key=lambda x: x[1], reverse=True)
    sorted_club_ids=[obj[0] for obj in sorted_recommended_clubs]
    object_data_lookup = {obj["id"]: obj for obj in serializer.data}

    recommended_clubs = [object_data_lookup[id] for id in sorted_club_ids]

    for club in recommended_clubs:
            club["profile_picture"]="http://localhost:8000"+club["profile_picture"]

    return recommended_clubs




    
    