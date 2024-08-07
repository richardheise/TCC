function [eigenDropPercent,totalTime] = greedyPlacement(A,matrixLength,deletionCount,score,lam1)
    tic;
    score_prime=[];
    score_new=[];
    selectedNodes=zeros(deletionCount,1);
    eigenDropPercent=0;

    alpha=max(score);
    score_prime=alpha*score.^2;
    score_prime;

   
        
    score_new=[];
    idx_2=find(score==max(score));
    selectedNodes(1)=idx_2(1);

    for i=2:deletionCount               
        B2=A(:,selectedNodes(1:i-1));
        b2= (B2 * score(selectedNodes(1:i-1)));
        score_new=score_prime - 2 *(b2.*score);             
        score_new(selectedNodes(1:i-1))=-1;
        idx_2=find(score_new==max(score_new));
        selectedNodes(i)=idx_2(1);           
    end   
    
    totalTime=toc;

    
    opts.disp = 0;
    A0 = A;
    A0(:,selectedNodes) = 0;
    A0(selectedNodes,:) = 0;
    [u00, lam00] = eigs(A0, 1,'LM',opts);
    lam00=abs(lam00);
    del = lam1 - lam00;
    eigenDropPercent=(del/lam1)*100;
    
    end