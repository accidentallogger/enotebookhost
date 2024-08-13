from django.shortcuts import render
from enotebooktool.models import reactionTable, reactionScheme
from django.http import HttpResponse, JsonResponse


def save_reaction_data(request):
    if request.method == "POST" and "savelocal" in str(request.body):
        print(request.body)
        try:
            option = request.POST.get("option")
            compound = request.POST.get("compound")
            weight = request.POST.get("actualWgt")
            molecular_weight = request.POST.get("weight")
            molecular_formula = request.POST.get("m_f")
            moles = request.POST.get("moles")
            ratio = request.POST.get("ratio")
            density = request.POST.get("density")
            
            # Save to the appropriate model based on the option selected
            if option == "option1":  # Reactant
                reactionTable.objects.create(
                    compound=compound,
                    molecular_weight=molecular_weight,
                    weight=weight,
                    molecular_formula=molecular_formula,
                    moles=moles,
                    ratio=ratio,
                    density=density,
                )
            elif option == "option2":  # Product
                reactionTable.objects.create(
                    compound=compound,
                    molecular_weight=molecular_weight,
                    weight=weight,
                    molecular_formula=molecular_formula,
                    moles=moles,
                    ratio=ratio,
                    density=density,
                )
            elif option == "option3":  # Solvent
                reactionScheme.objects.create(solvent=compound)
            elif option == "option4":  # Catalyst
                reactionScheme.objects.create(catalyst=compound)

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error"}, status=400)


def notebookview(request):
    #save_reaction_data(request)
    return render(request, "enotebook/main_new.html")
