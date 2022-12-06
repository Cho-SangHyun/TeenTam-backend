from boards.models import Boards

def BookmarkValidation(boards_id):
    
    boards = Boards.objects.filter(id=boards_id).first()
    if not boards or boards.delete_date:
        return False
    return True