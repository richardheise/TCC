function [eigenDropPercent,total_time] = NetshieldTime(A,k,idx_out)
%%%find k nodes, and if we delete them, will produce maximum drop in terms
%%%of the 1st eigen-value of A
%%%greedy way by matrix perturbation theory and submodularity
%A is the given graph
%k is the number of nodes to delete
%idx is the index of deleted nodes
%del is the difference of 1st eigen-value of A after deleting the nodes
tic;
if nargin<3
    idx_out = [];
end
if k<0
    idx = -1;
    return;
end


%%%pre-processing? (e.g., to exclude those degree-1 nodes)

opts.disp = 0;
[u, lam] = eigs(A, 1,'LM',opts);
lam=abs(lam);
% make sure all elements of u positive
pos = find(abs(u)==max(abs(u)));
if u(pos(1)) < 0
	u = -u ;
end

time=0;

n = size(A,1);

% tic;
u0 = (2 * lam * ones(n,1) - diag(A)).*(u.^2);
%top 1
tmp = u0;
tmp(idx_out)=-1;
pos = find(tmp==max(tmp));
idx = pos(1);

%%%greedily find the other nodes
for i=2:k
    A0 = A(:,idx);
    tmp = A0 * u(idx);
    tmp = u0 - 2 * (tmp.*u);
    tmp(idx) = -1;%exclude those already selected
    tmp(idx_out) = -1;
    pos = find(tmp==max(tmp));
    idx = [idx;pos(1)];
end

total_time=toc;
eigenDropPercent=0;
if nargout>1
    A0 = A;
    A0(:,idx) = 0;
    A0(idx,:) = 0;
    [u00, lam00] = eigs(A0, 1,'LM',opts);
    lam00=abs(lam00);
    del = lam - lam00;
    eigenDropPercent=(del/lam)*100;
    %fprintf('%s%0.5f%s%0.5f%s%0.5f\n','NetSheild : ',lam,'-',lam00,' = ',del);
end


