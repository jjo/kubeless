FUNCNAME=pubsub-python

$(FUNCNAME): k8s-events-sync
	kubeless function ls |grep -wq $(FUNCNAME) || \
	  kubeless function deploy $(FUNCNAME) --trigger-topic k8s \
	    --from-file botevents.py --handler botevents.handler \
	    --runtime python2.7 --dependencies requirements.txt
	kubectl get pod

k8s-events-sync: events-rbac
	kubeless topic ls |grep -q k8s || kubeless topic create k8s
	kubectl get deployment k8s-events-sync >/dev/null 2>&1 || \
	  kubectl run k8s-events-sync --image=skippbox/k8s-events:0.10.12

events-rbac:
	kubectl apply -f events-rbac.yaml

$(FUNCNAME)-logs:
	kubectl logs -l function=$(FUNCNAME)

$(FUNCNAME)-verify:
	kubectl get pod -l function=$(FUNCNAME)
	kubectl get namespace events-test-foobar 2>/dev/null || \
	  kubectl create namespace events-test-foobar
	$(MAKE) $(FUNCNAME)-logs |grep events-test-foobar
	
clean:
	-kubeless function delete $(FUNCNAME)
	-kubectl delete deployment $(FUNCNAME)
	-kubectl delete deployment k8s-events-sync
	-kubectl delete -f events-rbac.yaml
	-kubectl delete namespace events-test-foobar 2>/dev/null
