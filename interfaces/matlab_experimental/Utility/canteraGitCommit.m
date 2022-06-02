function v = canteraGitCommit()
    % Get Cantera Git commit hash
    % canteraGitCommit()
    %
    % :return:
    %     A string containing the Git commit hash for the current version of Cantera
    %
    checklib;
    buflen = calllib(ct, 'ct_getGitCommit', 0, '');
    aa = char(zeros(1, buflen));
    [~, aa] = calllib(ct, 'ct_getGitCommit', buflen, aa);
    v = aa;
end
